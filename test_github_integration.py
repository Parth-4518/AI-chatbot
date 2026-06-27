import os
import sys
import subprocess
import json

def run_cmd(cmd, cwd=None):
    """Run a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout, result.stderr

def test_git_config():
    """Test that git user config is set."""
    print("\n=== Test: Git Config ===")
    code, out, err = run_cmd("git config user.name && git config user.email")
    if code == 0:
        print("✅ Git config is set:")
        print(out)
        return True
    else:
        print("❌ Git config is missing:")
        print(err)
        return False

def test_github_remote(workspace):
    """Test that the GitHub remote is accessible."""
    print("\n=== Test: GitHub Remote ===")
    code, out, err = run_cmd("git remote -v", cwd=workspace)
    if code != 0:
        print("❌ Failed to list remotes:")
        print(err)
        return False
    
    print("Remotes found:")
    print(out)
    
    # Check if origin points to GitHub
    if "github.com" in out:
        print("✅ GitHub remote configured")
    else:
        print("⚠️ No GitHub remote found")
        return False
    
    # Test connectivity with ls-remote
    code, out, err = run_cmd("git ls-remote origin HEAD", cwd=workspace)
    if code == 0:
        print("✅ Can reach GitHub remote")
        return True
    else:
        print("❌ Cannot reach GitHub remote:")
        print(err)
        return False

def test_github_api(token):
    """Test GitHub API connectivity with a token."""
    print("\n=== Test: GitHub API ===")
    if not token:
        print("⚠️ No GH_TOKEN provided. Skipping API test.")
        return None
    
    import urllib.request
    req = urllib.request.Request(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            print(f"✅ GitHub API authenticated as: {data.get('login')}")
            return True
    except Exception as e:
        print(f"❌ GitHub API test failed: {e}")
        return False

def test_git_operations(workspace):
    """Test basic git operations (status, log)."""
    print("\n=== Test: Git Operations ===")
    code, out, err = run_cmd("git status --short", cwd=workspace)
    if code == 0:
        print("✅ Git status works")
        if out.strip():
            print("Uncommitted changes:")
            print(out)
        else:
            print("Working tree clean")
    else:
        print("❌ Git status failed:")
        print(err)
        return False
    
    code, out, err = run_cmd("git log --oneline -5", cwd=workspace)
    if code == 0:
        print("✅ Git log works")
        print("Recent commits:")
        print(out)
        return True
    else:
        print("❌ Git log failed:")
        print(err)
        return False

def main():
    workspace = os.path.dirname(os.path.abspath(__file__))
    token = os.environ.get("GH_TOKEN", "")
    
    print("=" * 50)
    print("GitHub Integration Test Suite")
    print("=" * 50)
    
    results = []
    results.append(("Git Config", test_git_config()))
    results.append(("GitHub Remote", test_github_remote(workspace)))
    results.append(("Git Operations", test_git_operations(workspace)))
    results.append(("GitHub API", test_github_api(token)))
    
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    for name, result in results:
        status = "✅ PASS" if result else ("⚠️ SKIP" if result is None else "❌ FAIL")
        print(f"{name:20s} {status}")
    
    # Exit with error if any mandatory test failed
    mandatory = [r for n, r in results if r is not None]
    if all(mandatory):
        print("\n🎉 All GitHub integration tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed. Check output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
