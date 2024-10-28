# THIS WAS WRITTEN BY A BOZO
# DO NOT USE UNLESS YOU ARE ALSO A BOZO
#
#                                                   _  _
#                                                  (\\( \
#                                                   `.\-.)
#                               _...._            _,-'   `-.
# \                           ,'      `-._.---.,-'       .  \
#  \`.                      ,'                               `.
#   \ `-...__              /                           .   .:  y
#    `._     ``--..__     /                           ,'`---._/
#       `-._         ``--'                      |    /_
#           `.._                   _            ;   <_ \
#               `--.___             `.           `-._ \ \
#                      `--<           `.     (\ _/)/ `.\/
#                          \            \     `
#
# He doens't have feet. I'm sorry.

#!/usr/bin/env python3

from random import randint
import math
from typing import Tuple
from warnings import deprecated


@deprecated("This algorithm runs in exponential time. You shouldn't use it.")
def dumb_is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def factor_2(n: int) -> Tuple[int, int]:
    """
    Factor out powers of 2 from n.
    Return (d, s) where n = d*2^s and d is odd.
    """
    acc = 0
    while n % 2 == 0:
        acc += 1
        n //= 2
    return (n, acc)


def is_prime(n: int) -> bool:
    """
    Uses the Miller-Rabin primality test, which is probabilistic.

    The number of rounds used determines the probability with which a given
    composite number will be accidentally labelled prime. For most numbers,
    that probability will be 8^(-k) as the tested number `n` grows.
    """
    if n <= 1:
        raise ValueError("n must be greater than 1.")
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # write n - 1 as d * 2^s where d is odd
    (d, s) = factor_2(n - 1)

    def try_witness(a: int) -> bool:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            # composite
            # nontrivial square root of 1 modulo n
            return False

        for _ in range(0, s - 1):
            x = (x * x) % n

            if x == n - 1:
                return True
            if x == 1:
                return False

        return x == 1

    k = 32  # 32 rounds

    for _ in range(0, k):
        a = randint(2, n - 2)
        if not try_witness(a):
            return False

    # probably prime
    return True


def generate_prime(length: int) -> int:
    min_val = 2 ** (length - 1)
    max_val = 2**length - 1
    prime = randint(min_val, max_val)
    while not is_prime(prime):
        prime = randint(min_val, max_val)
    return prime


def mod_inverse(e: int, n: int) -> int:
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """Extended Euler's algorithm"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(e, n)

    if gcd != 1:
        raise ValueError("no modular inverse exists")

    return x % n


def generate_rsa_primes(length: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    p = generate_prime(length)
    q = generate_prime(length)

    # make sure the primes aren't the same
    while p == q:
        q = generate_prime(length)

    # calculate phi
    phi = (q - 1) * (p - 1)

    # calculate n
    n = p * q

    # find e
    e = randint(2, phi)
    while math.gcd(e, phi) != 1:
        e = randint(2, phi)

    # compute d
    d = mod_inverse(e, phi)

    pubkey = (n, e)
    privkey = (n, d)

    return pubkey, privkey

def main():
    (p, q) = generate_rsa_primes(2048)
    print(p, q)


if __name__ == "__main__":
    main()