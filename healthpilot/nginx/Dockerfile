FROM nginx:1.21-alpine

# removed default config and add our new config to file
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d