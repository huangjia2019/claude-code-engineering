const express = require('express');
const router = express.Router();
const { requireAuth, isAdmin } = require('../middleware/auth');
const { validate } = require('../middleware/validate');
const { productSchema } = require('../schemas/product');

// GET /api/products - List all products (public)
router.get('/', async (req, res) => {
  const { page = 1, limit = 20, category } = req.query;
  const filters = category ? { category } : {};
  const products = await req.db.products.findAll({ page, limit, ...filters });
  res.json({ data: products, page, limit });
});

// GET /api/products/:id - Get product detail (public)
router.get('/:id', async (req, res) => {
  const product = await req.db.products.findById(req.params.id);
  if (!product) return res.status(404).json({ error: 'Product not found' });
  res.json({ data: product });
});

// POST /api/products - Create product (admin only)
router.post('/', requireAuth, isAdmin, validate(productSchema), async (req, res) => {
  const product = await req.db.products.create(req.body);
  res.status(201).json({ data: product });
});

// PUT /api/products/:id - Update product (admin only)
router.put('/:id', requireAuth, isAdmin, validate(productSchema), async (req, res) => {
  const product = await req.db.products.update(req.params.id, req.body);
  if (!product) return res.status(404).json({ error: 'Product not found' });
  res.json({ data: product });
});

// DELETE /api/products/:id - Delete product (admin only)
router.delete('/:id', requireAuth, isAdmin, async (req, res) => {
  await req.db.products.delete(req.params.id);
  res.status(204).send();
});

// Chained route: /api/products/:id/reviews
router.route('/:id/reviews')
  .get(async (req, res) => {
    const reviews = await req.db.reviews.findByProduct(req.params.id);
    res.json({ data: reviews });
  })
  .post(requireAuth, validate(reviewSchema), async (req, res) => {
    const review = await req.db.reviews.create({
      ...req.body,
      productId: req.params.id,
      userId: req.user.id,
    });
    res.status(201).json({ data: review });
  });

module.exports = router;
