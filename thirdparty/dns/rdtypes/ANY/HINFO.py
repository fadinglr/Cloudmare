# Copyright (C) Dnspython Contributors, see LICENSE for text of ISC license

# Copyright (C) 2003-2007, 2009-2011 Nominum, Inc.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose with or without fee is hereby granted,
# provided that the above copyright notice and this permission notice
# appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND NOMINUM DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL NOMINUM BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import struct

import thirdparty.dns.exception
import thirdparty.dns.rdata
import thirdparty.dns.tokenizer


class HINFO(thirdparty.dns.rdata.Rdata):

    """HINFO record"""

    # see: RFC 1035

    __slots__ = ['cpu', 'os']

    def __init__(self, rdclass, rdtype, cpu, os):
        super().__init__(rdclass, rdtype)
        if isinstance(cpu, str):
            object.__setattr__(self, 'cpu', cpu.encode())
        else:
            object.__setattr__(self, 'cpu', cpu)
        if isinstance(os, str):
            object.__setattr__(self, 'os', os.encode())
        else:
            object.__setattr__(self, 'os', os)

    def to_text(self, origin=None, relativize=True, **kw):
        return '"{}" "{}"'.format(thirdparty.dns.rdata._escapify(self.cpu),
                                  thirdparty.dns.rdata._escapify(self.os))

    @classmethod
    def from_text(cls, rdclass, rdtype, tok, origin=None, relativize=True,
                  relativize_to=None):
        cpu = tok.get_string(max_length=255)
        os = tok.get_string(max_length=255)
        tok.get_eol()
        return cls(rdclass, rdtype, cpu, os)

    def _to_wire(self, file, compress=None, origin=None, canonicalize=False):
        l = len(self.cpu)
        assert l < 256
        file.write(struct.pack('!B', l))
        file.write(self.cpu)
        l = len(self.os)
        assert l < 256
        file.write(struct.pack('!B', l))
        file.write(self.os)

    @classmethod
    def from_wire_parser(cls, rdclass, rdtype, parser, origin=None):
        cpu = parser.get_counted_bytes()
        os = parser.get_counted_bytes()
        return cls(rdclass, rdtype, cpu, os)
