from typing import List, Optional, Union

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
    gif100px: Optional[ContentUrlsContent]
    largeGif: Optional[ContentUrlsContent]
    max1mbGif: Optional[ContentUrlsContent]
    max2mbGif: Optional[ContentUrlsContent]
    max5mbGif: Optional[ContentUrlsContent]
    mobile: Optional[ContentUrlsContent]
    mobilePoster: Optional[ContentUrlsContent]
    mp4: Optional[ContentUrlsContent]
    webm: Optional[ContentUrlsContent]
    webp: Optional[ContentUrlsContent]


class GfyItem(BaseModel):
    avgColor: Color
    content_urls: ContentUrls
    createDate: str
    description: Optional[str]
    frameRate: Union[conint(gt=0), confloat(gt=0)]
    gatekeeper: int
    gfyId: str
    gfyName: str
    gfyNumber: str
    gfySlug: Optional[str]
    gif100px: Optional[AnyHttpUrl]
    gifUrl: Optional[AnyHttpUrl]
    hasAudio: bool
    hasTransparency: bool
    height: conint(gt=0)
    isSticker: bool
    languageCategories: List[Optional[str]]
    likes: conint(ge=0)
    max1mbGif: AnyHttpUrl
    max2mbGif: AnyHttpUrl
    max5mbGif: AnyHttpUrl
    md5: str
    miniPosterUrl: Optional[AnyHttpUrl]
    miniUrl: AnyHttpUrl
    mobilePosterUrl: Optional[AnyHttpUrl]
    mobileUrl: Optional[AnyHttpUrl]
    nsfw: conint(ge=0)
    numFrames: conint(gt=0)
    posterUrl: Optional[str]
    published: conint(ge=0)
    tags: List[Optional[str]]
    thumb100PosterUrl: Optional[AnyHttpUrl]
    title: Optional[str]
    userData: Optional[UserData]
    userDisplayName: Optional[str]
    username: str
    userProfileImageUrl: Optional[AnyHttpUrl]
    views: conint(ge=0)
    webmSize: confloat(gt=0)
    webmUrl: Optional[AnyHttpUrl]
    webpUrl: AnyHttpUrl
    width: conint(gt=0)
