# Tweet ship arrivals with image via X API v2
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class TwitterPoster:
    def __init__(self, bearer_token=None, api_key=None,
                 api_secret=None, access_token=None,
                 access_token_secret=None):
        self.bearer = bearer_token
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.has_auth = any([bearer_token, api_key])
        if not self.has_auth:
            logger.warning('Twitter creds not set - dry run only')

    def _load_tweepy(self):
        try:
            import tweepy
            return tweepy
        except ImportError:
            logger.error('tweepy not installed')
            raise

    def post_tweet(self, text, image_path=None):
        if not self.has_auth:
            logger.info('[DRY RUN] Would post: %s', text[:100])
            if image_path:
                logger.info('[DRY RUN] With image: %s', image_path)
            return dict(dry_run=True, text=text)
        tweepy = self._load_tweepy()
        client = tweepy.Client(
             bearer_token=self.bearer,
            consumer_key=self.api_key,
           consumer_secret=self.api_secret,
          access_token=self.access_token,
         access_token_secret=self.access_token_secret)
        media_id = None
        if image_path and Path(image_path).exists():
            try:
                with open(image_path, 'rb') as fh:
                    bdata = fh.read()
                resp = client.upload_media(tweepy.MediaField(media=bdata))
                media_id = resp.media_key
                logger.info('Media uploaded (id=%s)', media_id)
            except Exception as exc:
                logger.warning('Image upload failed, text only: %s', exc)
        try:
            tw_text = text[:450]
            result = client.create_tweet(text=tw_text,
                     media_ids=[media_id] if media_id else None)
            tid = result.data.get('id')
            logger.info('Tweet posted: id=%s', tid)
            return dict(success=True, tweet_id=tid)
        except Exception as exc:
            logger.error('Tweet failed: %s', exc)
            return dict(success=False, error=str(exc))

    @staticmethod
    def build_enter_text(name, imo=None, flag=None, length_m=None):
        nl = chr(10)
        parts = ['New ship entering Port of A Coruna!']
        parts.append(nl + 'Vessel: ' + str(name))
        if imo:
            parts.append('IMO: ' + str(imo))
        if flag:
            parts.append('Flag: ' + str(flag))
        if length_m:
            parts.append('Length: ' + str(length_m) + 'm')
        parts.append(nl + '#AIS #Acoruna #HarborWatch')
        return nl.join(parts)

    @staticmethod
    def build_docked_text(name, imo=None, zone_name='docking area'):
        nl = chr(10)
        parts = [str(name) + ' now docked at ' + str(zone_name)]
        if imo:
            parts.append('IMO: ' + str(imo))
        parts.append(nl + '#AIS #Acoruna #HarborWatch')
        return nl.join(parts)
