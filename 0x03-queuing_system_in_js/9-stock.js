const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const client = redis.createClient();

const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

const listProducts = [
    { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
    { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
    {"itemId":3,"itemName":"Suitcase 650","price":350, initialAvailableQuantity:2},
    {"itemId":4,"itemName":"Suitcase 1050","price":550,"initialAvailableQuantity":5}
];

function getItemById(id) {
    return listProducts.find(product => product.itemId === id);
}

async function reserveStockById(itemId, stock) {
    await setAsync(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
    const reservedStock = await getAsync(`item.${itemId}`);
    return parseInt(reservedStock) || 0;
}

app.get('/list_products', (req, res) => {
    res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
    const { itemId } = req.params;
    const product = getItemById(parseInt(itemId));
    if (!product) {
        res.status(404).json({ status: 'Product not found' });
        return;
    }
    const currentQuantity = await getCurrentReservedStockById(parseInt(itemId));
    res.json({ ...product, currentQuantity });
});

app.get('/reserve_product/:itemId', async (req, res) => {
    const { itemId } = req.params;
    const product = getItemById(parseInt(itemId));
    if (!product) {
        res.status(404).json({ status: 'Product not found' });
        return;
    }
    const currentQuantity = await getCurrentReservedStockById(parseInt(itemId));
    if (currentQuantity >= product.initialAvailableQuantity) {
        res.json({ status: 'Not enough stock available', itemId: parseInt(itemId) });
        return;
    }
    await reserveStockById(parseInt(itemId), currentQuantity + 1);
    res.json({ status: 'Reservation confirmed', itemId: parseInt(itemId) });
});

const PORT = 1245;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
