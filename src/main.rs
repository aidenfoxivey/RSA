// DON'T USE THIS!!!!
// IT'S PURELY EDUCATIONAL

use num_bigint::{BigUint, RandBigInt};
use num_traits::One;
use rand::thread_rng;

struct RSAPubKey((BigUint, BigUint));
struct RSAPrivKey((BigUint, BigUint));

fn generate_rsa_primes(length: usize) -> (BigUint, BigUint) {
    // Since 2015, NIST recommends a minimum of 2048-bit keys for RSA.
    if length < 2048 {
        eprintln!("Caution! NIST recommends a minimum size of 2048-bit keys for RSA.");
    }

    let n = length / 2;

    let two = BigUint::from(2u32);
    let lower_bound = two.pow((n - 1) as u32);
    let upper_bound = two.pow(n as u32) - BigUint::one();

    let p = get_prime(&lower_bound, &upper_bound);

    let mut q;

    loop {
        q = get_prime(&lower_bound, &upper_bound);

        if suitable_rsa_pair(&p, &q) {
            break;
        }
    }

    (p, q)
}

fn get_prime(lower: &BigUint, upper: &BigUint) -> BigUint {
    const ROUNDS: usize = 64;
    let mut rng = thread_rng();
    let mut candidate;

    loop {
        candidate = rng.gen_biguint_range(lower, upper);

        if miller_rabin_test::<ROUNDS>(&candidate) {
            break;
        }
    }

    candidate
}

fn try_witness(witness: &BigUint, n: &BigUint, s: &BigUint, d: &BigUint) -> bool {
    let mut x = witness.modpow(d, n);

    if x == BigUint::one() || x == BigUint::from(n - 1u32) {
        return false;
    }

    // fails if we don't have an appropriately sized BigUint
    for _ in 0..(s - BigUint::one()).try_into().unwrap() {
        x = x.modpow(&BigUint::from(2u32), n);

        if x == BigUint::from(n - 1u32) {
            return true;
        }

        if x == BigUint::one() {
            return false;
        }
    }

    x == BigUint::one()
}

fn miller_rabin_test<const ROUNDS: usize>(candidate: &BigUint) -> bool {
    if *candidate <= BigUint::one() {
        return false;
    }

    if *candidate == BigUint::from(2u32) {
        return true;
    }

    // If even and not two, then we conclude it to be odd.
    if (candidate % BigUint::from(2u32)) == BigUint::ZERO {
        return false;
    }

    let mut rng = thread_rng();

    // get the factors we need
    let mut d = candidate - BigUint::one();
    let mut s = 0u32;

    while (d.clone() % BigUint::from(2u32)) == BigUint::ZERO {
        d >>= 1u32;
        s += 1;
    }

    for _ in 0..ROUNDS {
        let witness =
            rng.gen_biguint_range(&BigUint::from(2u32), &(candidate - BigUint::from(2u32)));

        if !try_witness(&witness, candidate, &BigUint::from(s), &d) {
            return false;
        }
    }

    // probably prime
    true
}

fn generate_rsa_keys(length: usize) -> (RSAPubKey, RSAPrivKey) {
    let (p, q) = generate_rsa_primes(length);

    let phi = (&q - BigUint::from(1u32)) * (&p - BigUint::from(1u32));

    let n = BigUint::from(&q * &p);

    let e;
    let d;

    (RSAPubKey((n, e)), RSAPrivKey((n, d)))
}

fn suitable_rsa_pair(p: &BigUint, q: &BigUint) -> bool {
    true
}

fn main() {
    println!("{:?}", generate_rsa_primes(64));
}
