#!/bin/bash

YELLOW='\033[1;31m'
SEA='\033[38;5;49m'
NC='\033[0m'

#addi variable of script location
location=$(dirname "$0")
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PARENT="$(dirname "$SCRIPT_DIR")"

DCFLAGS="-Wall -fno-common -Wextra -Wno-missing-field-initializers"
DCXXFLAGS="-Wno-ignored-attributes"

compile() {

  echo "Compile: $@" 1>&2
  make distclean || echo clean
  rm -f config.status
  ./autogen.sh || echo done
  CFLAGS="-O3 -march=${1} ${3} ${DCFLAGS}" \
  CXXFLAGS="$CFLAGS -std=c++20 ${DCXXFLAGS}" \
  ./configure --with-curl
  make -j $(nproc)
  strip -s cpuminer
  #mv cpuminer cwork-${2}
  NEW=python3-${2}
  mkdir "../work"
  echo $NEW > ../work/new.txt
  mv cpuminer $PARENT/work/$NEW
}



LSCPU=$(lscpu)
MODEL_NAME=$(lscpu | egrep "Model name" | tr -s " " | cut -d":" -f 2-)

if lscpu | egrep -i "GenuineIntel" 1>/dev/null; then
  CPU_VENDOR="Intel"
  echo -n "Detected Intel CPU: "
elif lscpu | egrep -i "AuthenticAMD" 1>/dev/null; then
  CPU_VENDOR="AMD"
  CPU_FAMILY=$(lscpu | egrep -o -i "CPU family: +[0-9]+" | awk '{ print $3 }')
  if [[ $CPU_FAMILY == 25 ]]; then
    ZEN="zen3"
    echo -n "Detected AMD zen3 CPU: "
  elif [[ $CPU_FAMILY == 23 ]]; then
    CPU_MODEL=$(lscpu | egrep -o -i "Model: +[0-9]+" | awk '{ print $2 }')
    if [[ $CPU_MODEL == 1 || $CPU_MODEL == 17 || \
          $CPU_MODEL == 24 || $CPU_MODEL == 32 ]]; then
      ZEN="zen"
      echo -n "Detected AMD zen CPU: "
    elif [[ $CPU_MODEL == 8 || $CPU_MODEL == 24 ]]; then
      ZEN="zen+"
      echo -n "Detected AMD zen+ CPU: "
    elif [[ $CPU_MODEL == 49  || $CPU_MODEL == 71 || $CPU_MODEL == 96  || \
            $CPU_MODEL == 104 || $CPU_MODEL == 113 || $CPU_MODEL == 144 ]]; then
      ZEN="zen2"
      echo -n "Detected AMD zen2 CPU: "
    else
      echo -n "Detected AMD non-ZEN CPU: "
    fi
  fi
else
  CPU_VENDOR="Unknown"
  echo -n "Detected Unknown CPU: "
fi
echo -e "${SEA}${MODEL_NAME}${NC}"

echo -ne "Available CPU Instructions: ${SEA}"

# Check AVX512 / AVX2 / AVX / SSE4.2
if lscpu | egrep -i " avx512f( |$)" 1>/dev/null && \
   lscpu | egrep -i " avx512dq( |$)" 1>/dev/null && \
   lscpu | egrep -i " avx512bw( |$)" 1>/dev/null && \
   lscpu | egrep -i " avx512vl( |$)" 1>/dev/null; then
  HAS_AVX512=1
  echo -n "AVX512 "
fi
if lscpu | egrep -i " avx2( |$)" 1>/dev/null; then
  HAS_AVX2=1
  echo -n "AVX2 "
fi
if lscpu | egrep -i " avx( |$)" 1>/dev/null; then
  HAS_AVX=1
  echo -n "AVX "
fi
if lscpu | egrep -i " sse4_2( |$)" 1>/dev/null; then
  HAS_SSE42=1
  echo -n "SSE42 "
fi

# Check VAES / AES
if lscpu | egrep -i " vaes( |$)" 1>/dev/null; then
  HAS_VAES=1
  echo -n "VAES "
fi
if lscpu | egrep -i " aes(_ni|-ni)?( |$)" 1>/dev/null; then
  HAS_AES=1
  echo -n "AES "
fi

# Check SHA
if lscpu | egrep -i " sha(_ni)?( |$)" 1>/dev/null; then
  HAS_SHA=1
  echo -n "SHA "
fi
echo -e "${NC}"


if [[ $HAS_AVX512 && $HAS_SHA && $HAS_VAES ]]; then
  INST="avx512-sha-vaes"
elif [[ $HAS_AVX512 && $HAS_SHA && $HAS_AES ]]; then
  INST="avx512-sha-aes"
elif [[ $HAS_AVX512 && $HAS_AES ]]; then
  INST="avx512-aes"
elif [[ $HAS_AVX2 && $HAS_AES ]]; then
  INST="avx2-aes"
fi

if [[ $INST == "avx512-sha-vaes" ]]; then
  echo "# Icelake AVX512 SHA VAES  @avx512-sha-vaes"
  compile "icelake-client" "avx512-sha-vaes" "-mtune=intel"
elif [[ $INST == "avx512-sha-aes" ]]; then
  echo "# Rocketlake AVX512 SHA AES @avx512-sha-aes"
  compile "cascadelake" "avx512-sha" "-msha -mtune=intel"
elif [[ $INST == "avx512-aes" ]]; then
  echo "# Slylake-X AVX512 AES  @avx512-aes"
  compile "skylake-avx512" "avx512" "-mtune=intel"
elif [[ $INST == "avx2-aes" ]]; then
  echo "#AVX2+ # Haswell AVX2 AES  @avx2-aes"
  # GCC 9 doesn't include AES with core-avx2
  compile "core-avx2" "avx2" "-maes"
fi
