py.test --cov-config .coveragerc \
        --cov-report html \
        --cov ../embervite
python -c "import webbrowser, os; \
           webbrowser.open('file://' + os.getcwd() + \
                           '/.coverage_html/index.html')"
