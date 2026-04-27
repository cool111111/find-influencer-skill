# Platform Selectors & Commands Reference

Quick reference for each supported platform's search commands, DOM selectors, and data extraction patterns.

## Xiaohongshu (小红书)

### opencli Commands

```bash
# Search notes
opencli xiaohongshu search "<keyword>" --limit 20 -f json

# Get user profile notes
opencli xiaohongshu user <user_id> -f json

# Get feed
opencli xiaohongshu feed --limit 20 -f json
```

Note: `search` may require login. If blocked, use Playwright fallback.

### Search URL Template

```
https://www.xiaohongshu.com/search_result?keyword=<url_encoded>&type=1&sort=popularity_descending
```

### Playwright: Extract Search Results

```javascript
() => {
  const noteItems = document.querySelectorAll('[class*="note-item"]');
  return Array.from(noteItems).map(el => {
    const titleEl = el.querySelector('.title');
    const authorEl = el.querySelector('.author');
    const likeCount = el.querySelector('[class*="like"] [class*="count"], .like-wrapper .count, .count');
    const link = el.querySelector('a[href*="/explore/"]');
    const authorLink = el.querySelector('a.author');
    const authorId = authorLink?.href?.match(/profile\/([^?]+)/)?.[1];
    return {
      title: titleEl?.textContent?.trim(),
      author: authorEl?.textContent?.trim(),
      likes: likeCount?.textContent?.trim(),
      url: link?.href,
      authorId
    };
  }).filter(item => item.title);
}
```

### Playwright: Extract Profile Stats

```javascript
() => {
  const allText = document.body.innerText;
  const followMatch = allText.match(/(\d[\d,.万]*)\s*粉丝/);
  const likeMatch = allText.match(/(\d[\d,.万]*)\s*获赞与收藏/);
  const nameEl = document.querySelector('[class*="user-name"]');
  const bio = document.querySelector('[class*="desc"]')?.textContent?.trim();

  const notes = [];
  const noteItems = document.querySelectorAll('[class*="note-item"], section[class*="note"]');
  noteItems.forEach(el => {
    const title = el.querySelector('[class*="title"], .footer-info .title')?.textContent?.trim();
    const likes = el.querySelector('[class*="like"] [class*="count"], .count')?.textContent?.trim();
    if (title) notes.push({ title, likes });
  });

  return {
    name: nameEl?.textContent?.trim(),
    followers: followMatch?.[1],
    totalLikes: likeMatch?.[1],
    bio: bio?.substring(0, 100),
    topNotes: notes.slice(0, 10)
  };
}
```

### Playwright: Close Login Modal

```javascript
() => {
  const closeBtn = document.querySelector('.login-container .close-button, .login-modal .close-button, [class*="close"]');
  if (closeBtn) { closeBtn.click(); return 'closed'; }
  const modal = document.querySelector('.reds-modal.login-modal');
  if (modal) { modal.remove(); return 'removed'; }
  return 'no modal';
}
```

### Profile URL

```
https://www.xiaohongshu.com/user/profile/<user_id>
```

### Note URL

```
https://www.xiaohongshu.com/explore/<note_id>
```

---

## Bilibili (B站)

### opencli Commands

```bash
# Search videos
opencli bilibili search --keyword "<keyword>" --limit 20 -f json

# Hot videos
opencli bilibili hot --limit 20 -f json

# User info (if supported)
opencli bilibili user <uid> -f json
```

### Search URL Template

```
https://search.bilibili.com/all?keyword=<url_encoded>&order=click
```

### Key Selectors (Playwright fallback)

```javascript
// Search results
'.video-list .video-item, .search-page .video-item'

// Video stats
'.video-data span'  // play count, danmaku count
'.up-name'          // author name

// User profile
'.n-statistics .n-data-v'  // follower count
```

### Profile URL

```
https://space.bilibili.com/<uid>
```

---

## Douyin (抖音)

### No opencli support - use Playwright only

### Search URL Template

```
https://www.douyin.com/search/<url_encoded>?type=video
```

### Key Selectors

```javascript
// Search results (may change frequently)
'[class*="search-result"] [class*="video-card"]'

// Author info
'[class*="author-card"]'

// Stats
'[class*="like-count"], [class*="comment-count"]'
```

### Profile URL

```
https://www.douyin.com/user/<sec_uid>
```

---

## YouTube

### opencli Commands

```bash
# Search videos
opencli youtube search --query "<keyword>" --limit 20 -f json
```

### Search URL Template

```
https://www.youtube.com/results?search_query=<url_encoded>&sp=CAMSAhAB
# sp=CAMSAhAB = sort by view count
```

---

## TikTok

### opencli Commands

```bash
# Search videos
opencli tiktok search "<keyword>" --limit 20 -f json

# Get user profile (followers, likes, bio)
opencli tiktok profile <username> -f json

# Get recent videos from user
opencli tiktok user <username> --limit 20 -f json
```

### Profile URL

```
https://www.tiktok.com/@<username>
```

### Key Fields from opencli

- `profile`: `followers`, `likes`, `bio`, `username`
- `user`: `title`, `views`, `likes`, `date`, `url`

---

## X (Twitter)

### opencli Commands

```bash
# Search tweets
opencli twitter search "<keyword>" --limit 20 -f json

# Get user profile (followers, bio, tweet count)
opencli twitter profile <username> -f json

# Get followers list
opencli twitter followers <username> -f json
```

### Profile URL

```
https://x.com/<username>
```

### Key Fields from opencli

- `profile`: `followers`, `following`, `tweets`, `bio`, `joined`
- `search`: `author`, `text`, `likes`, `retweets`, `date`, `url`

---

## Instagram

### opencli Commands

```bash
# Search users by keyword
opencli instagram search "<keyword>" --limit 20 -f json

# Get user profile (followers, posts count, bio)
opencli instagram profile <username> -f json

# Get recent posts from user
opencli instagram user <username> --limit 20 -f json
```

### Profile URL

```
https://www.instagram.com/<username>/
```

### Key Fields from opencli

- `profile`: `followers`, `following`, `posts`, `bio`, `is_verified`
- `user`: `likes`, `comments`, `url`, `date`, `caption`

---

### Batch Profile Visiting (any platform)

```javascript
async (page) => {
  const profiles = [
    { name: 'creator1', id: 'xxx' },
    { name: 'creator2', id: 'yyy' },
  ];
  const results = [];
  for (const p of profiles) {
    await page.goto(`${BASE_URL}${p.id}`, { waitUntil: 'domcontentloaded', timeout: 10000 });
    await page.waitForTimeout(2000);
    const data = await page.evaluate(EXTRACT_FUNCTION);
    results.push({ ...p, ...data });
  }
  return results;
}
```

### Video Frame Capture

```javascript
async (page) => {
  // Navigate to video post
  await page.goto(videoUrl, { waitUntil: 'domcontentloaded', timeout: 12000 });
  await page.waitForTimeout(3000);

  // Try to play
  const playBtn = await page.$('[class*="play"], .player-container, video');
  if (playBtn) await playBtn.click();

  // Capture frames at intervals
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'frame1.png' });
  await page.waitForTimeout(4000);
  await page.screenshot({ path: 'frame2.png' });
  await page.waitForTimeout(4000);
  await page.screenshot({ path: 'frame3.png' });
}
```
