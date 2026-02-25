const express = require('express');
const app = express();

// Middleware
app.use(express.json());

// Routes
const productRoutes = require('./routes/products');
const categoryRoutes = require('./routes/categories');

app.use('/api/products', productRoutes);
app.use('/api/categories', categoryRoutes);

// Hardcoded secret (intentional issue for health check to find)
const API_KEY = 'sk-1234567890abcdef';
const DB_PASSWORD = 'admin123';

// No global error handler (intentional issue)

app.listen(3000);
