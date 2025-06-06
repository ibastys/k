from __future__ import annotations

from typing import TYPE_CHECKING

from pyk.kast import Atts, KAtt
from pyk.kast.inner import KToken
from pyk.kast.outer import KClaim, KRule
from pyk.kast.prelude.kbool import BOOL
from pyk.kast.prelude.ml import is_top, mlOr
from pyk.testing import KProveTest

from ..utils import K_FILES

if TYPE_CHECKING:
    from pyk.ktool.kprove import KProve


class TestSimpleProof(KProveTest):
    KOMPILE_MAIN_FILE = K_FILES / 'simple-proofs.k'
    KOMPILE_ARGS = {'syntax_module': 'SIMPLE-PROOFS'}

    def test_prove_claim_with_lemmas(self, kprove: KProve) -> None:
        # Given
        claim = KClaim(
            KToken('<k> foo => bar ... </k> <state> 3 |-> 3 </state>', 'TCellFragment'),
            requires=KToken('pred1(4)', BOOL),
        )
        lemma = KRule(
            KToken('pred1(3) => true', BOOL),
            requires=KToken('pred1(4)', BOOL),
            att=KAtt(entries=[Atts.SIMPLIFICATION(None)]),
        )

        # When
        result1 = kprove.prove_claim(claim, 'claim-without-lemma')
        result2 = kprove.prove_claim(claim, 'claim-with-lemma', lemmas=[lemma])

        # Then
        assert not is_top(mlOr([res.kast for res in result1]), weak=True)
        assert is_top(mlOr([res.kast for res in result2]), weak=True)
