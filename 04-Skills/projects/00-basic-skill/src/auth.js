/**
 * 认证模块 - 故意包含安全问题供审查练习
 * WARNING: 这是教学示例，不要用于生产环境！
 */

// 问题 1: 硬编码的密钥
const SECRET_KEY = 'super-secret-key-12345';
const API_KEY = 'sk-live-abcdef123456';

// 问题 2: 弱密码验证
function validatePassword(password) {
  // 只检查长度，没有复杂度要求
  return password.length >= 6;
}

// 问题 3: 不安全的 token 生成
function generateToken(userId) {
  // 使用可预测的方式生成 token
  const timestamp = Date.now();
  return Buffer.from(`${userId}:${timestamp}`).toString('base64');
}

// 问题 4: 明文存储密码比较
function checkPassword(inputPassword, storedPassword) {
  // 应该使用 bcrypt 等哈希比较
  return inputPassword === storedPassword;
}

// 问题 5: 信息泄露的错误消息
function login(username, password) {
  const user = findUserByUsername(username);

  if (!user) {
    // 泄露用户是否存在
    throw new Error(`User '${username}' not found`);
  }

  if (!checkPassword(password, user.password)) {
    // 应该使用统一的错误消息
    throw new Error('Invalid password');
  }

  return {
    token: generateToken(user.id),
    // 问题 6: 返回过多用户信息
    user: {
      id: user.id,
      username: user.username,
      email: user.email,
      password: user.password,  // 不应该返回密码！
      role: user.role,
      internalNotes: user.internalNotes  // 内部信息泄露
    }
  };
}

// 问题 7: 无会话过期
function verifyToken(token) {
  const decoded = Buffer.from(token, 'base64').toString();
  const [userId, timestamp] = decoded.split(':');
  // 没有检查 token 是否过期
  return { userId, timestamp };
}

// 问题 8: eval 使用
function processUserConfig(configString) {
  // 危险！允许代码注入
  return eval('(' + configString + ')');
}

// 模拟函数
function findUserByUsername(username) {
  const users = {
    'admin': {
      id: 1,
      username: 'admin',
      password: 'admin123',  // 弱密码
      email: 'admin@example.com',
      role: 'admin',
      internalNotes: 'Super user with all permissions'
    }
  };
  return users[username];
}

module.exports = {
  validatePassword,
  generateToken,
  checkPassword,
  login,
  verifyToken,
  processUserConfig,
  SECRET_KEY,
  API_KEY
};
