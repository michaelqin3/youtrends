-- We used Flask SQLAlchemy as our application ORM 
-- We have translated our code into raw SQL syntax

-- The code that performs these queries can be found in `code/youtube-trends-backend/app/routes.py`, we recommend viewing this file
-- as some queries utilize external variables such as from user input, which cannot be modeled precisely here. 

-- DESCRIPTION: get top 10 videos 
-- SQL ALCHEMY: videos = models.Video.query.all()
SELECT * FROM video LIMIT 10;

-- DESCRIPTION: get top 10 videos ordered by views in descending order
-- SQL ALCHEMY: videos = models.Video.query.order_by(models.Video.views.desc()).all()
SELECT * FROM video ORDER BY video.views DESC LIMIT 10;

-- DESCRIPTION: get top 10 playlists 
-- SQL ALCHEMY: playlists = models.Playlist.query.all()
SELECT * FROM playlist LIMIT 10;


-- DESCRIPTION: get all playlist videos
SELECT * FROM playlist_video;
-- No need to limit since there is only 1 tuple

-- DESCRIPTION: get all videos that are also in a playlist
-- SQL ALCHEMY: 
--     videos = models.Video.query\
--     .join(PlaylistVideo, models.Video.id == models.PlaylistVideo.video_id)
--     .filter_by(PlaylistVideo.playlist_id == id)
SELECT video.* FROM video, playlist_video 
WHERE video.id=playlist_video.video_id;
-- No need to limit since only 1 is returned in our example

-- DESCRIPTION: Index trending_country and publish_time attributes for more efficiency
CREATE INDEX country_index ON video (trending_country);

CREATE INDEX publish_time_index ON video (publish_time);
