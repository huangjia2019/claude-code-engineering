const { add } = require("./math");
const assert = require("assert");

console.log("Running tests...\n");

// Test 1: should pass
try {
  assert.strictEqual(add(1, 2), 3);
  console.log("✓ add(1, 2) === 3");
} catch (e) {
  console.error("✗ add(1, 2) === 3");
  console.error("  " + e.message);
  process.exitCode = 1;
}

// Test 2: fixed
try {
  assert.strictEqual(add(2, 3), 5);
  console.log("✓ add(2, 3) === 5");
} catch (e) {
  console.error("✗ add(2, 3) === 5");
  console.error("  " + e.message);
  process.exitCode = 1;
}

console.log("\nDone.");
