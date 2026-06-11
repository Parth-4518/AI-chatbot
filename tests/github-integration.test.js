const { describe, it, expect } = require('@jest/globals');
const fs = require('fs');
const path = require('path');

describe('GitHub Integration', () => {
  const repoRoot = path.resolve(__dirname, '..');

  it('should have a README.md file', () => {
    const readmePath = path.join(repoRoot, 'README.md');
    expect(fs.existsSync(readmePath)).toBe(true);
  });

  it('should have a .gitignore file', () => {
    const gitignorePath = path.join(repoRoot, '.gitignore');
    expect(fs.existsSync(gitignorePath)).toBe(true);
  });

  it('should have a GitHub Actions workflow', () => {
    const workflowPath = path.join(repoRoot, '.github', 'workflows', 'verify-integration.yml');
    expect(fs.existsSync(workflowPath)).toBe(true);
  });

  it('README should contain project title', () => {
    const readmePath = path.join(repoRoot, 'README.md');
    const content = fs.readFileSync(readmePath, 'utf8');
    expect(content).toMatch(/AI Chatbot/i);
  });
});
