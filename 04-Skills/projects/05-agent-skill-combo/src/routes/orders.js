const express = require('express');
const router = express.Router();
const { requireAuth } = require('../middleware/auth');
const { validate } = require('../middleware/validate');
const { orderSchema } = require('../schemas/order');

// GET /api/orders - List current user's orders
router.get('/', requireAuth, async (req, res) => {
  const orders = await req.db.orders.findByUser(req.user.id);
  res.json({ data: orders });
});

// GET /api/orders/:id - Get order detail
router.get('/:id', requireAuth, async (req, res) => {
  const order = await req.db.orders.findById(req.params.id);
  if (!order) return res.status(404).json({ error: 'Order not found' });
  if (order.userId !== req.user.id) return res.status(403).json({ error: 'Forbidden' });
  res.json({ data: order });
});

// POST /api/orders - Create new order
router.post('/', requireAuth, validate(orderSchema), async (req, res) => {
  const order = await req.db.orders.create({
    ...req.body,
    userId: req.user.id,
    status: 'pending',
  });
  res.status(201).json({ data: order });
});

// Chained route example: /api/orders/:id/status
router.route('/:id/status')
  .get(requireAuth, async (req, res) => {
    const order = await req.db.orders.findById(req.params.id);
    if (!order) return res.status(404).json({ error: 'Order not found' });
    res.json({ status: order.status });
  })
  .put(requireAuth, async (req, res) => {
    const order = await req.db.orders.updateStatus(req.params.id, req.body.status);
    res.json({ data: order });
  });

module.exports = router;
