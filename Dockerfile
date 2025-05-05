FROM sridhar281994/buildozer-android:v10
# Auto-confirm root prompt
RUN sed -i "s/cont = input('Are you sure you want to continue [y/n]?')/cont = 'y'/" \
    $(python3 -c "import buildozer, os; p = buildozer.__file__.replace('__init__.pyc', '__init__.py'); print(p)")
