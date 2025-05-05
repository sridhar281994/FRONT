FROM sridhar281994/buildozer-android:v10
# Patch Buildozer to auto-accept root prompt
RUN python3 -c "\
import buildozer; \
f = buildozer.__file__; \
with open(f, 'r') as file: \
    content = file.read(); \
content = content.replace(\"cont = input('Are you sure you want to continue [y/n]?')\", \"cont = 'y'\"); \
with open(f, 'w') as file: \
    file.write(content)"
WORKDIR /app
# Copy your application files into the container
COPY . /app
