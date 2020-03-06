#! /bin/bash
oldDir=$(pwd)
LIBDIR="/disc/Document/lib/" # TODO : changer ça pour que ça ne soit pas en dur

if [[ $# -eq 1 && $1 == "clean" ]]; then
    rm $LIBDIR/test/fragment_shader01.fs
    exit 0
fi

if [[ $# -ne 2 ]]; then
    echo "Syntax : $0 [shader] [2D|3D]"
    exit 1
fi


if [[ -e "$LIBDIR/shaders/noises/$1/fragment_shader$2.fs" ]]; then

    cd $LIBDIR/test/
    cp $LIBDIR/shaders/noises/$1/fragment_shader$2.fs .
    mv fragment_shader$2.fs fragment_shader01.fs
    python viewer.py
    cd $oldDir
    exit 0
else
    echo "Shader $1 doesn't exist"
    echo "Current existing noise shaders : "
    cd $LIBDIR/shaders/noises/
    for i in $(find . -mindepth 1 -maxdepth 1 -type d  \( ! -iname ".*" \) | sed 's|^\./||g'); do
        echo "  $i"; # TODO : add dimension dispo
    done
    cd $oldDir
    # TODO : Add autres types de shaders here
    exit 1
fi
