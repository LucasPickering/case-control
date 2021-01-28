# Rust doesn't have an arm32v6 image so we have to just use debian
FROM debian:stable-slim AS builder

ENV PATH="$PATH:$HOME/.cargo/bin"
ENV TARGET=arm-unknown-linux-gnueabihf

RUN apt-get update && \
    apt-get install -y curl
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o rustup.sh
RUN sh rustup.sh -y
# RUN apt-get uninstall -y curl && \
#     rm -rf /var/lib/apt/lists/*
WORKDIR /app/api
RUN rustup target add $TARGET
COPY rust-toolchain .
RUN sh -c "rustup toolchain add $(cat rust-toolchain)"
COPY . .
RUN cargo build --release --target=$TARGET

FROM debian:stable-slim
WORKDIR /app/api
COPY --from=builder /app/api/target/release/soze-api .
CMD ["/app/api/soze-api"]
