
FROM rust AS source
COPY . .

FROM source AS test
RUN cargo test

FROM source AS build
RUN RUSTFLAGS='-C target-feature=+crt-static'\
    cargo build --release

FROM scratch
COPY --from=build ./target/release/attempt .
CMD ["./attempt"]

