const express = require('express');
const router = express.Router();
const db = require('../utils/db');

// GET /api/categories
router.get('/', async (req, res) => {
  try {
    const categories = await db.query('SELECT * FROM categories');
    res.json({ data: categories });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/categories
router.post('/', async (req, res) => {
  try {
    const category = await db.query(
      'INSERT INTO categories SET ?',
      req.body
    );
    res.status(201).json({ data: category });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Duplicated validation logic (intentional - same as products.js)
function validateCategory(data) {
  if (!data.name || typeof data.name !== 'string') return false;
  if (!data.description || typeof data.description !== 'string') return false;
  return true;
}

// Unused function (intentional issue)
function formatCategory(cat) {
  return { id: cat.id, name: cat.name, slug: cat.name.toLowerCase() };
}

module.exports = router;
