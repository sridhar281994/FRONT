FROM sridhar281994/buildozer-android:v10
# Patch Buildozer to skip root prompt safely
RUN echo '\
import buildozer\n\
f = buildozer.__file__\n\
with open(f, "r") as file:\n\
    content = file.read()\n\
content = content.replace("cont = input(\'Are you sure you want to continue [y/n]?\')", "cont = \'y\'")\n\
with open(f, "w") as file:\n\
    file.write(content)\n\
' > /tmp/patch.py && python3 /tmp/patch.py
WORKDIR /app
COPY . /app
