const express = require('express');
const router = express.Router();
const { requireAuth, isAdmin } = require('../middleware/auth');
const { validate } = require('../middleware/validate');
const { userSchema, updateUserSchema } = require('../schemas/user');

// GET /api/users - List all users (admin only)
router.get('/', requireAuth, isAdmin, async (req, res) => {
  const { page = 1, limit = 20 } = req.query;
  const users = await req.db.users.findAll({ page, limit });
  res.json({ data: users, page, limit });
});

// GET /api/users/:id - Get user by ID
router.get('/:id', requireAuth, async (req, res) => {
  const user = await req.db.users.findById(req.params.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json({ data: user });
});

// POST /api/users - Create new user
router.post('/', validate(userSchema), async (req, res) => {
  const user = await req.db.users.create(req.body);
  res.status(201).json({ data: user });
});

// PUT /api/users/:id - Update user
router.put('/:id', requireAuth, validate(updateUserSchema), async (req, res) => {
  const user = await req.db.users.update(req.params.id, req.body);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json({ data: user });
});

// DELETE /api/users/:id - Delete user (admin only)
router.delete('/:id', requireAuth, isAdmin, async (req, res) => {
  await req.db.users.delete(req.params.id);
  res.status(204).send();
});

module.exports = router;
