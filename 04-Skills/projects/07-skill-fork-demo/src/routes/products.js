const express = require('express');
const router = express.Router();
const db = require('../utils/db');

// GET /api/products - List products
router.get('/', async (req, res) => {
  // No try/catch (intentional issue)
  const products = await db.query('SELECT * FROM products');
  res.json({ data: products });
});

// GET /api/products/:id - Get product by ID
router.get('/:id', async (req, res) => {
  try {
    // SQL injection vulnerability (intentional issue)
    const product = await db.query(
      `SELECT * FROM products WHERE id = ${req.params.id}`
    );
    if (!product) return res.status(404).json({ error: 'Not found' });
    res.json({ data: product });
  } catch (err) {
    // Error swallowed - no response sent (intentional issue)
    console.log(err);
  }
});

// POST /api/products - Create product
router.post('/', async (req, res) => {
  try {
    // No input validation (intentional issue)
    const product = await db.query(
      'INSERT INTO products SET ?',
      req.body
    );
    res.status(201).json({ data: product });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// PUT /api/products/:id - Update product
router.put('/:id', async (req, res) => {
  try {
    const product = await db.query(
      'UPDATE products SET ? WHERE id = ?',
      [req.body, req.params.id]
    );
    res.json({ data: product });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE /api/products/:id - Delete product
router.delete('/:id', async (req, res) => {
  try {
    await db.query('DELETE FROM products WHERE id = ?', [req.params.id]);
    res.status(204).send();
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Duplicated validation logic (intentional issue - same pattern as categories.js)
function validateProduct(data) {
  if (!data.name || typeof data.name !== 'string') return false;
  if (!data.price || typeof data.price !== 'number') return false;
  if (data.price < 0) return false;
  return true;
}

module.exports = router;
