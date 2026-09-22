# 3. Fix unsafe direct startup

| [Previous: security planning](2-security-planning.md) | [Next: dependencies](4-dependencies.md) |
|:---|---:|

Budget: 17 minutes. The shelter API passes its tests but starts with debugging enabled when `app.py` is run directly.

## Why it matters

CodeQL's `py/flask-debug` rule identifies a configuration that can expose the Werkzeug debugger. A regression test makes the intended startup behavior explicit. This small fix does not turn Flask's development server into a production server.

## Try it

1. Inspect the baseline **Flask app is run in debug mode** finding and its path, `app/server/app.py`. Confirm that the source ends with `app.run(debug=True, port=5100)`. If the finding is absent or the code differs, use [troubleshooting](take-home/troubleshooting.md) before changing anything.
2. Select branch `exercise/shelter-change` in your learner repository. Edit `app/server/app.py` and change only the final call:

   ```python
   if __name__ == '__main__':
       app.run(debug=False, port=5100) # Port 5100 to avoid macOS conflicts
   ```

3. In `app/server/test_app.py`, add the following method inside `class TestApp`, before `if __name__ == '__main__':`. Keep its four-space indentation. A copyable [test snippet](solutions/startup-test.py.txt) is also supplied.

   ```python
       def test_direct_startup_disables_debug(self):
           import os
           from pathlib import Path
           import runpy

           with patch.dict(os.environ, {'DATABASE_PATH': ':memory:', 'FLASK_DEBUG': '1'}):
               with patch('flask.Flask.run') as run:
                   runpy.run_path(str(Path(__file__).with_name('app.py')), run_name='__main__')

           run.assert_called_once_with(debug=False, port=5100)
   ```

4. Commit both changes to the existing branch. In the web editor, two commits are fine; evaluate the last one with both edits. Do not create a new PR or commit these edits to `main`. Terminal users can use:

   ```bash
   git switch exercise/shelter-change
   git add -- app/server/app.py app/server/test_app.py
   git diff --cached
   git commit -m "Disable direct debug startup and test the default"
   git push
   ```

5. Confirm CI and CodeQL started for the updated PR. Continue to dependencies while analysis runs. Check back at the start of lesson 4 and during the demonstrations.

The test intercepts `Flask.run`; it never opens a socket. It uses an in-memory database and sets `FLASK_DEBUG=1` deliberately, proving the explicit safe default wins. Do not edit `app/scripts/common.sh`: its debug setting belongs to the existing local-development route. Deliberate local debugging remains available through the Flask CLI. Neither route is a production deployment recipe.

## Checkpoint

Record the final fix commit and its successful functional checks. Inspect the PR's CodeQL results for that revision and confirm the targeted finding no longer appears. The default-branch alert may remain open while your PR is unmerged; take-home Lab 1 checks its closure after merge.

The supplied regression test fails against `debug=True` and passes against `debug=False`; you still need the GitHub results above. See [solutions](solutions/README.md) for the explanation. Leave your working PR open.

## Resources

[CodeQL: Flask app is run in debug mode](https://codeql.github.com/codeql-query-help/python/py-flask-debug/) documents the rule and severity. [Flask deployment guidance](https://flask.palletsprojects.com/en/stable/deploying/) explains why its development server should not serve production traffic.

| [Previous: security planning](2-security-planning.md) | [Next: dependencies](4-dependencies.md) |
|:---|---:|
