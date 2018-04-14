#! /usr/bin/env python3
# This script generates the token.h header file.

header = """/* Auto-generated by Tools/scripts/generate_token_h.py */

/* Token types */
#ifndef Py_LIMITED_API
#ifndef Py_TOKEN_H
#define Py_TOKEN_H
#ifdef __cplusplus
extern "C" {
#endif

#undef TILDE   /* Prevent clash of our definition with system macro. Ex AIX, ioctl.h */

"""

footer = """
/* Special definitions for cooperation with parser */

#define ISTERMINAL(x)           ((x) < NT_OFFSET)
#define ISNONTERMINAL(x)        ((x) >= NT_OFFSET)
#define ISEOF(x)                ((x) == ENDMARKER)


PyAPI_DATA(const char * const) _PyParser_TokenNames[]; /* Token names */
PyAPI_FUNC(int) PyToken_OneChar(int);
PyAPI_FUNC(int) PyToken_TwoChars(int, int);
PyAPI_FUNC(int) PyToken_ThreeChars(int, int, int);

#ifdef __cplusplus
}
#endif
#endif /* !Py_TOKEN_H */
#endif /* Py_LIMITED_API */
"""


def load_module(path):
    module = type('Namespace', (), {})()
    with open(path, 'rb') as fp:
        code = fp.read()
    exec(code, module.__dict__)
    return module

def main(token_py='Lib/token.py', outfile='Include/token.h'):
    token = load_module(token_py)
    tok_name = token.tok_name
    with open(outfile, 'w') as fobj:
        fobj.write(header)
        for value in sorted(tok_name):
            if token.ERRORTOKEN < value < token.N_TOKENS:
                continue
            name = tok_name[value]
            fobj.write("#define %-15s %d\n" % (name, value))
        fobj.write(footer)
    print("%s regenerated from %s" % (outfile, token_py))


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
