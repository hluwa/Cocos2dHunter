# Author: hluwa <hluwa888@gmail.com>
# HomePage: https://github.com/hluwa
# CreatedTime: 4/21/20 21:21


import os
import sys
from gzip import GzipFile
from io import BytesIO

import click

import xxtea


def find_targets(path):
    result = []
    if not os.path.exists(path):
        return []
    if not os.path.isdir(path):
        return [path]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jsc"):
                result.append(os.path.join(root, file))
    return result


def main(path, key, force=False):
    result = []
    targets = find_targets(path)
    for target in targets:
        out = target[:-1]
        if os.path.exists(out) and force:
            click.secho("file is existed, please use `-f` to overwrite it: {}".format(out), fg="yellow")
            result.append(out)
            continue

        content = open(target, "rb").read()
        if key:
            key=bytes(key,encoding='utf-8')
            content = xxtea.decrypt(content, key)

        if content[:2] == b'\037\213':
            try:
                mock_fp = BytesIO(content)
                gz = GzipFile(fileobj=mock_fp)
                content = gz.read()
            except Exception as e:
                import traceback
                click.secho("ungz fault {} in {}".format(e, traceback.format_tb(sys.exc_info()[2])[-1]), fg="red")

        with open(out, 'wb') as _:
            _.write(content)

        click.secho("decrypt successful: {}".format(out), fg="green")
        result.append(out)
    return result


main(sys.argv[1], sys.argv[2])
