const express = require('express');
const router = express.Router();
const { requireAuth, isAdmin } = require('../middleware/auth');

// GET /api/categories - List all categories (public)
router.get('/', async (req, res) => {
  const categories = await req.db.categories.findAll();
  res.json({ data: categories });
});

// GET /api/categories/:id - Get category with products (public)
router.get('/:id', async (req, res) => {
  const category = await req.db.categories.findById(req.params.id);
  if (!category) return res.status(404).json({ error: 'Category not found' });
  const products = await req.db.products.findByCategory(req.params.id);
  res.json({ data: { ...category, products } });
});

// POST /api/categories - Create category (admin only)
router.post('/', requireAuth, isAdmin, async (req, res) => {
  const category = await req.db.categories.create(req.body);
  res.status(201).json({ data: category });
});

// PUT /api/categories/:id - Update category (admin only)
router.put('/:id', requireAuth, isAdmin, async (req, res) => {
  const category = await req.db.categories.update(req.params.id, req.body);
  if (!category) return res.status(404).json({ error: 'Category not found' });
  res.json({ data: category });
});

// DELETE /api/categories/:id - Delete category (admin only)
router.delete('/:id', requireAuth, isAdmin, async (req, res) => {
  const productCount = await req.db.products.countByCategory(req.params.id);
  if (productCount > 0) {
    return res.status(409).json({
      error: 'Cannot delete category with existing products',
    });
  }
  await req.db.categories.delete(req.params.id);
  res.status(204).send();
});

module.exports = router;
