use std::usize;

use itertools::Itertools;

fn good(subset: &[usize], frbdn: &[usize]) -> bool {
    subset.windows(2).all(|v| !frbdn.contains(&(v[1] - v[0])))
}

fn good_global(subset: &[usize]) -> bool {
    itertools::iproduct!(subset, subset, subset)
        .all(|(a, b, c)| (a + 2 * b) as isize - (3 * c) as isize != 6)
}

fn main() {
    let s_0 = (0..42).step_by(3);
    let s_1 = (1..42).step_by(3);
    let s_2 = (2..42).step_by(3);

    let s = [s_0, s_1, s_2];

    let mut valid: [[Vec<Vec<usize>>; 6]; 3] = Default::default();

    for (i, s_i) in s.iter().enumerate() {
        valid[i][0] = [vec![]].to_vec();
        valid[i][1] = s_i.clone().map(|x| [x].to_vec()).collect();

        (2..=5).for_each(|k| {
            valid[i][k] = s_i
                .clone()
                .combinations(k)
                .filter(|subset| good(subset, &[3, 6]))
                .collect();
        });
    }

    let pairs = [[5, 5, 2], [5, 4, 3], [4, 4, 4]];

    let mut violating: Vec<Vec<usize>> = Vec::default();

    pairs
        .iter()
        .flat_map(|p| p.iter().permutations(3))
        .unique()
        .for_each(|v| {
            itertools::iproduct!(&valid[0][*v[0]], &valid[1][*v[1]], &valid[2][*v[2]]).for_each(
                |(e_1, e_2, e_3)| {
                    let mut testset: Vec<usize> = e_1
                        .iter()
                        .chain(e_2.iter().chain(e_3.iter()))
                        .copied()
                        .collect();

                    testset.sort();

                    if good(&testset, &[2]) && good_global(&testset) {
                        violating.push(testset);
                    }
                },
            );
        });
    println!("{violating:?}")
}
