from typing import Optional

from pydantic import AnyHttpUrl, BaseModel, confloat, conint
from pydantic.color import Color


class UserData(BaseModel):
    followers: conint(ge=0)
    following: conint(ge=0)
    name: str
    profileImageUrl: AnyHttpUrl
    subscription: conint(ge=0)
    username: str
    verified: bool
    views: conint(ge=0)


class ContentUrlsContent(BaseModel):
    url: AnyHttpUrl
    size: confloat(gt=0)
    width: conint(gt=0)
    height: conint(gt=0)


class ContentUrls(BaseModel):
    gif100px: ContentUrlsContent
    largeGif: ContentUrlsContent
    max1mbGif: ContentUrlsContent
    max2mbGif: ContentUrlsContent
    max5mbGif: ContentUrlsContent
    mobile: ContentUrlsContent
    mobilePoster: ContentUrlsContent
    mp4: ContentUrlsContent
    webm: ContentUrlsContent
    webp: ContentUrlsContent


class GfyItem(BaseModel):
    avgColor: Color
    content_urls: ContentUrls
    createDate: str
    description: str
    frameRate: conint(gt=0) | confloat(gt=0)
    gatekeeper: int
    gfyId: str
    gfyName: str
    gfyNumber: str
    gfySlug: str
    gif100px: AnyHttpUrl
    gifUrl: AnyHttpUrl
    hasAudio: bool
    hasTransparency: bool
    height: conint(gt=0)
    isSticker: bool
    languageCategories: list[Optional[str]]
    likes: conint(ge=0)
    max1mbGif: AnyHttpUrl
    max2mbGif: AnyHttpUrl
    max5mbGif: AnyHttpUrl
    md5: str
    miniPosterUrl: AnyHttpUrl
    miniUrl: AnyHttpUrl
    mobilePosterUrl: AnyHttpUrl
    mobileUrl: AnyHttpUrl
    nsfw: conint(ge=0)
    numFrames: conint(gt=0)
    posterUrl: str
    published: conint(ge=0)
    tags: list[Optional[str]]
    thumb100PosterUrl: AnyHttpUrl
    title: str
    userData: UserData
    userDisplayName: str
    username: str
    userProfileImageUrl: AnyHttpUrl
    views: conint(ge=0)
    webmSize: confloat(gt=0)
    webmUrl: AnyHttpUrl
    webpUrl: AnyHttpUrl
    width: conint(gt=0)
