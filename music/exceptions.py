from rest_framework import status

from moyeora_connector.responses import ErrorResponse

MUSIC_REQUEST_SONG_INVALID = ErrorResponse(
    code='MUSIC_REQUEST_SONG_INVALID',
    status=status.HTTP_200_OK,
    message='신청곡 양식이 일치하지 않습니다.'
)

MUSIC_UNAUTHORIZED = ErrorResponse(
    code='MUSIC_UNAUTHORIZED',
    status=status.HTTP_401_UNAUTHORIZED,
    message='신청곡 편집에 권한이 없습니다.'
)

MUSIC_REQUEST_SONG_NOTFOUND = ErrorResponse(
    code='MUSIC_REQUEST_SONG_NOTFOUND',
    status=status.HTTP_200_OK,
    message='요청하는 신청곡을 찾을 수 없습니다.'
)

MUSIC_HISTORY_SONG_NOTFOUND = ErrorResponse(
    code='MUSIC_HISTORY_SONG_NOTFOUND',
    status=status.HTTP_200_OK,
    message='요청하는 신청 기록을 찾을 수 없습니다.'
)

MUSIC_SONG_COMMENTS_INVALID = ErrorResponse(
    code = 'MUSIC_SONG_COMMENTS_INVALID',
    status=status.HTTP_400_BAD_REQUEST,
    message='댓글 양식이 일치하지 않습니다.'
)

MUSIC_SONG_COMMENTS_NOTFOUND = ErrorResponse(
    code = 'MUSIC_SONG_COMMENTS_NOTFOUND',
    status=status.HTTP_200_OK,
    message='요청하는 댓글 기록을 찾을 수 없습니다.'
)

MUSIC_SONG_LIKE_INVALID = ErrorResponse(
    code = 'MUSIC_SONG_LIKE_INVALID',
    status=status.HTTP_200_OK,
    message='좋아요 양식이 일치하지 않습니다.'
)

MUSIC_SONG_LIKE_SAME_USER = ErrorResponse(
    code = 'MUSIC_SONG_LIKE_SAME_USER',
    status=status.HTTP_200_OK,
    message='자신의 신청곡에 좋아요를 누를 수 없습니다.'
)

MUSIC_PLAY_EMPTY = ErrorResponse(
    code = 'MUSIC_PLAY_EMPTY',
    status=status.HTTP_200_OK,
    message="재생 가능한 신청곡이 없습니다."
)

MUSIC_PLAY_INVALID = ErrorResponse(
    code = 'MUSIC_PLAY_INVALID',
    status=status.HTTP_200_OK,
    message="노래 신청 양식이 일치하지 않습니다."
)