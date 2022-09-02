from typing import Optional

from pydantic import AnyHttpUrl, BaseModel, conint


class AlbumNode(BaseModel):
    id: str
    title: str
    linkText: str
    nsfw: conint(ge=0)
    folderSubType: str
    coverImageUrl: AnyHttpUrl
    coverImageUrlMobile: AnyHttpUrl
    width: conint(gt=0)
    height: conint(gt=0)
    mp4Url: AnyHttpUrl
    webmUrl: AnyHttpUrl
    webpUrl: AnyHttpUrl
    mobileUrl: AnyHttpUrl
    mobilePosterUrl: AnyHttpUrl
    posterUrl: AnyHttpUrl
    thumb360Url: AnyHttpUrl
    thumb360PosterUrl: AnyHttpUrl
    thumb100PosterUrl: AnyHttpUrl
    max5mbGif: AnyHttpUrl
    max2mbGif: AnyHttpUrl
    miniUrl: AnyHttpUrl
    miniPosterUrl: AnyHttpUrl
    mjpgUrl: AnyHttpUrl
    gifUrl: AnyHttpUrl
    published: conint(ge=0)
    nodes: list[Optional["AlbumNode"]]
