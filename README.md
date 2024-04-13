# podcasts-list-to-rss

Generate an RSS file from Telegram podcasts list

[bit.ly/podcastsrss](https://bit.ly/podcastsrss)

### What was done

- Read messages from Telegram channel
- Parse each message and get it's episode link
- Find the RSS link of the podcast and get the RSS item from it
- Build an RSS file from all items from all messages
- Use the original episode XML item and just update those fields:
  - Publish date - use the Telegram published date instead of the original episode published date
  - Prepand to episode's description the Telegram message description from
- Commit and save the RSS file
- Run this flow each 1 hour using GitHub Actions


### Next steps (Todo list)

- [x] Some messages are not well parsed and failing to get episode details
- [ ] Remember last read message and read only newer messages
- [ ] Update commit only if there are new episodes
- [ ] Use bot token to listen to new messages instead. Now we use app token that has more permissions and can read all channel history
- [ ] Different between this repo (which should be a template) and a specific repo for each desired flow, that can be managed by each user who wants to use this flow
- [ ] Support more podcasts sites (currently support only Pocket Casts)
