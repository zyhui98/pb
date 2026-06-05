# -*- coding: utf-8 -*-
"""
    model
    ~~~~~

    the paste model.

    :copyright: Copyright (C) 2015 by the respective authors; see AUTHORS.
    :license: GPLv3, see LICENSE for details.
"""

from hashlib import sha1
from mimetypes import guess_extension
from uuid import uuid4

from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.urls import url_quote, url_unquote

from pb.db import get_fs
from pb.paste.handler import handlers, label


def _transform(kwargs):
    for key, value in kwargs.items():
        if value is None:
            continue

        if key == 'content' or value is False:
            continue

        if key == 'redirect':
            key = 's'

        yield key, value


def transform(kwargs):
    return dict(_transform(kwargs))


def _put(stream):
    b = stream.read()
    digest = sha1(b).hexdigest()
    size = len(b)
    
    if size > 2 ** 23:
        b = get_fs().put(b)
    
    return dict(
        content=b,
        digest=digest,
        short=digest[-6:],
        size=size
    )


def _get(content):
    if isinstance(content, ObjectId):
        return get_fs().get(content).read()
    return content


def insert(stream, **kwargs):
    kwargs.update(**_put(stream))
    d = dict(
        _id=uuid4().hex,
        date=datetime.utcnow(),
        **transform(kwargs)
    )
    get_fs().db.pastes.insert_one(d)
    return d


def get_paste(short, show='auto'):
    paste = get_fs().db.pastes.find_one({'short': short})
    if not paste:
        return

    return render(paste, show)


def render(paste, show='auto'):
    if paste.get('redirect'):
        return paste

    paste['content'] = _get(paste['content'])

    if not isinstance(paste['content'], str):
        paste['content'] = paste['content'].decode()

    paste['mime'] = handlers.get(paste.get('handler', ''), label)
    paste['url'] = '/{}'.format(paste['short'])
    if 'sunset' in paste:
        paste['date'] = paste.pop('sunset')

    if show == 'direct-require':
        paste['show'] = 'direct'
    elif show == 'auto':
        paste['show'] = 'direct' if paste['mime'] != label else 'display'
    else:
        paste['show'] = 'display'

    paste['extension'] = guess_extension(
        paste['mime']) or '.txt'
    paste['label'] = label

    return paste


def delete_paste(digest, secret):
    return get_fs().db.pastes.delete_many({
        'digest': digest,
        'secret': secret
    }).deleted_count
