FROM eclipse-temurin:21-jre
ENV MB_PLUGINS_DIR=/plugins
RUN mkdir -p /plugins /app
ADD https://downloads.metabase.com/v0.49.13/metabase.jar /app/metabase.jar
EXPOSE 3000
CMD ["java", "-jar", "/app/metabase.jar"]