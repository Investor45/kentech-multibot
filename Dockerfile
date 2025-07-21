FROM quay.io/lyfe00011/md:beta
RUN git clone https://github.com/Investor45/kentech-multibot.git /root/KENTECH/
WORKDIR /root/LyFE/
RUN yarn install
CMD ["npm", "start"]