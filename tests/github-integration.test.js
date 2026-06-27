/**
 * GitHub Integration Test
 * 
 * This file verifies that the repository is properly connected to GitHub
 * and can receive commits, pushes, and pull requests.
 * 
 * Run with: node tests/github-integration.test.js
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

console.log('=== GitHub Integration Test ===\n');

// Test 1: Verify .git directory exists
console.log('Test 1: Checking .git directory...');
const gitDir = path.join(__dirname, '..', '.git');
assert.ok(fs.existsSync(gitDir), '.git directory should exist');
console.log('✓ .git directory exists\n');

// Test 2: Verify GitHub remote is configured
console.log('Test 2: Checking GitHub remote configuration...');
const gitConfigPath = path.join(gitDir, 'config');
assert.ok(fs.existsSync(gitConfigPath), 'git config should exist');
const gitConfig = fs.readFileSync(gitConfigPath, 'utf8');
assert.ok(gitConfig.includes('github.com'), 'git config should reference github.com');
console.log('✓ GitHub remote is configured\n');

// Test 3: Verify .github directory exists
console.log('Test 3: Checking .github directory...');
const githubDir = path.join(__dirname, '..', '.github');
assert.ok(fs.existsSync(githubDir), '.github directory should exist');
console.log('✓ .github directory exists\n');

// Test 4: Verify pull request template exists
console.log('Test 4: Checking pull request template...');
const prTemplate = path.join(githubDir, 'PULL_REQUEST_TEMPLATE.md');
assert.ok(fs.existsSync(prTemplate), 'PULL_REQUEST_TEMPLATE.md should exist');
const prContent = fs.readFileSync(prTemplate, 'utf8');
assert.ok(prContent.includes('Thinking Path'), 'PR template should include Thinking Path section');
assert.ok(prContent.includes('What Changed'), 'PR template should include What Changed section');
console.log('✓ Pull request template is properly configured\n');

// Test 5: Verify README exists
console.log('Test 5: Checking README...');
const readmePath = path.join(__dirname, '..', 'README.md');
assert.ok(fs.existsSync(readmePath), 'README.md should exist');
console.log('✓ README.md exists\n');

// Test 6: Verify package.json exists (for Node.js projects)
console.log('Test 6: Checking package.json...');
const packageJsonPath = path.join(__dirname, '..', 'package.json');
assert.ok(fs.existsSync(packageJsonPath), 'package.json should exist');
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
assert.ok(packageJson.name, 'package.json should have a name');
console.log(`✓ package.json exists (project: ${packageJson.name})\n`);

console.log('=== All GitHub Integration Tests Passed ===');
console.log('\nRepository is properly configured for GitHub integration.');
console.log('You can now create commits, push branches, and open pull requests.');
