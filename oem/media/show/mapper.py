from oem.core.match import EpisodeMatch


class ShowMapper(object):
    @classmethod
    def match(cls, show, season_num, episode_num, progress=None):
        if season_num is None:
            raise ValueError('Missing required parameter "season_num"')

        if episode_num is None:
            raise ValueError('Missing required parameter "episode_num"')

        # Default Season
        try:
            default_season = int(show.parameters['default_season'])
        except Exception:
            return None

        # Show
        best = EpisodeMatch(
            default_season,
            episode_num + int(show.parameters.get('episode_offset', 0))
        )

        # Season
        season, result = cls._match_season(show, season_num, episode_num)

        if result:
            best = result
        elif not season:
            return best

        # Episode
        result = cls._match_episode(season, episode_num, progress=progress)

        if result:
            best = result

        # Return best result
        return best

    @classmethod
    def _match_season(cls, show, season_num, episode_num):
        # Try retrieve matching season
        season = show.seasons.get(str(season_num))

        if not season:
            return None, None

        # Look for matching season mapping
        for season_mapping in season.mappings:
            if not (season_mapping.start <= episode_num <= season_mapping.end):
                continue

            return season, EpisodeMatch(
                int(season_mapping.season),
                episode_num + season_mapping.offset
            )

        return season, EpisodeMatch(
            season_num,
            episode_num
        )

    @classmethod
    def _match_episode(cls, season, episode_num, progress=None):
        episode = season.episodes.get(str(episode_num))

        if not episode:
            return None

        for episode_mapping in episode.mappings:
            # Parse timeline attributes
            if episode_mapping.timeline and 'source' in episode_mapping.timeline:
                if progress is None:
                    raise ValueError('Missing required parameter "progress"')

                timeline_source = episode_mapping.timeline['source']

                if not (timeline_source.start <= progress <= timeline_source.end):
                    # Ignore `episode_mapping`
                    continue

            # Parse mapping attributes
            try:
                season_num = int(episode_mapping.season)
            except:
                continue

            try:
                episode_num = int(episode_mapping.number)
            except:
                continue

            # Return episode match
            return EpisodeMatch(
                season_num,
                episode_num
            )

        return None
