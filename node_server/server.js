const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('AI Agent API Server Running');
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

// Webhook endpoint
app.post('/webhook', (req, res) => {
  console.log('Webhook received:', req.body);
  res.json({
    status: 'received',
    timestamp: new Date().toISOString(),
    data: req.body
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});