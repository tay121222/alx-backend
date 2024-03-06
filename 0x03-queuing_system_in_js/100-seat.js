import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const port = 1245;

const client = redis.createClient();
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

const queue = kue.createQueue();
let reservationEnabled = true;
const reserveSeat = async (number) => {
    await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
    const seats = await getAsync('available_seats');
    return seats;
};

const initializeSeats = async () => {
    await reserveSeat(50);
};

initializeSeats().then(() => {
    console.log('Seats initialized.');
}).catch((error) => {
    console.error('Error initializing seats:', error);
});

app.get('/available_seats', async (req, res) => {
    try {
        const availableSeats = await getCurrentAvailableSeats();
        res.json({ numberOfAvailableSeats: availableSeats });
    } catch (error) {
        res.status(500).json({ error: 'Error' });
    }
});

app.get('/reserve_seat', async (req, res) => {
    try {
        const reservationEnabled = true;
        if (!reservationEnabled) {
            return res.json({ status: 'Reservation are blocked' });
        }
        
        const job = queue.create('reserve_seat').save((err) => {
            if (err) {
                return res.json({ status: 'Reservation failed' });
            }
            res.json({ status: 'Reservation in process' });
        });
    } catch (error) {
        res.status(500).json({ error: 'Error' });
    }
});

app.get('/process', async (req, res) => {
    try {
        const currentSeats = await getCurrentAvailableSeats();
        if (currentSeats <= 0) {

            reservationEnabled = false;
            return res.json({ status: 'Queue processing', reservationEnabled });
        }

        queue.process('reserve_seat', async (job, done) => {
            const currentSeats = await getCurrentAvailableSeats();
            if (currentSeats <= 0) {
                return done(new Error('Not enough seats available'));
            }

            await reserveSeat(currentSeats - 1);
            if (currentSeats - 1 === 0) {
                reservationEnabled = false;
            }
            
            done();
        });
        
        res.json({ status: 'Queue processing', reservationEnabled });
    } catch (error) {
        res.status(500).json({ error: 'Error' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

