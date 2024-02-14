# Karin

A grumpy discord bot primarily aimed to supervise MKSwes new forum market.

### Current functions

- Validates that WTS posts contains at least one image
- Limits users to one post in WTS and one in WTB
- Archives the text contents of a deleted forum post
- Sends notice to users if they forget to include price in their WTS
- Runs a job to clean out old posts

## Overview of Environment Variables

This document provides an overview of the environment variables used in the Karin bot. Environment variables are used to configure and customize the behavior of the bot without altering the source code directly. Below is a list of the environment variables along with their descriptions:

| Environment Variable              | Description                                             |
| --------------------------------- | ------------------------------------------------------- |
| DISCORD_TOKEN                     | Bot token required for authentication with Discord API. |
| BUY_CHANNEL_ID                    | Channel ID where buy-related messages are posted.       |
| SELL_CHANNEL_ID                   | Channel ID where sell-related messages are posted.      |
| ARCHIVE_CHANNEL_ID                | Channel ID where archived messages are stored.          |
| PRICE_RECOMMENDATION_TITLE        | Title for price recommendation messages.                |
| PRICE_RECOMMENDATION_MESSAGE      | Message indicating a price recommendation.              |
| INVALID_REQUEST_TITLE             | Title for messages indicating an invalid request.       |
| THREAD_MUST_CONTAIN_IMAGE_MESSAGE | Message indicating that a thread must contain an image. |
| EXISTING_THREAD_ERROR_MESSAGE     | Message indicating an error due to an existing thread.  |
| OLD_THREAD_ALERT_TITLE            | Title for messages indicating a post is too old.        |
| OLD_THREAD_ALERT_BODY             | Message indicating a post is too old.                   |

## Description

- **DISCORD_TOKEN**: This token is required for the bot to authenticate itself with the Discord API. It's crucial for the bot's operation.

- **BUY_CHANNEL_ID**: Specifies the Channel ID where buy-related messages should be posted. This helps organize and streamline communication within the Discord server.

- **SELL_CHANNEL_ID**: Specifies the Channel ID where sell-related messages should be posted. Similar to `BUY_CHANNEL_ID`, this variable helps categorize communication.

- **ARCHIVE_CHANNEL_ID**: Denotes the Channel ID where archived messages are stored. This might be used for historical purposes or to keep the main channels clutter-free.

- **PRICE_RECOMMENDATION_TITLE**: Title used for price recommendation messages. This variable helps maintain consistency in message formatting.

- **PRICE_RECOMMENDATION_MESSAGE**: Message body indicating a price recommendation. It's a helpful prompt to encourage users to include prices in their posts.

- **INVALID_REQUEST_TITLE**: Title used for messages indicating an invalid request. This might be used to notify users when their requests do not meet certain criteria.

- **THREAD_MUST_CONTAIN_IMAGE_MESSAGE**: Message indicating that a thread must contain an image. It's a guideline for users to follow when creating threads.

- **EXISTING_THREAD_ERROR_MESSAGE**: Message indicating an error due to an existing thread. It's used to inform users when they already have an open thread in a specific category. Expected to contain the variables`{thread.name}`and `{thread.parent.name}`.

- **OLD_THREAD_ALERT_TITLE**: Title for messages indicating a post is too old. It's used to notify a users post has been removed due age.

- **OLD_THREAD_ALERT_BODY**: Message indicating a post is too old. It's used to explain in the notification why a users post has been removed.

Ensure that these environment variables are properly set and configured to enable the Karin bot to function correctly within your Discord server.
