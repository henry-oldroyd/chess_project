// the following functions execute add or subtract operations on a pair of vectors
function add_vectors(v1, v2) {
    // v1 + v2
    return [
        v1[0] + v2[0],
        v1[1] + v2[1],
    ]
}

function subtract_vectors(v1, v2) {
    // v1 - v2
    return [
        v1[0] - v2[0],
        v1[1] - v2[1],
    ]
}

// use arrays are equal method instead
// function vectors_are_equal(v1, v2) {
//     return JSON.stringify(v1.map(Number)) == JSON.stringify(v2.map(Number))
// }