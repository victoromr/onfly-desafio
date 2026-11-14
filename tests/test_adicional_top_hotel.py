"""Testes adicionais: critério de desempate no ranking de hotéis."""

from helpers import run_cli


def test_top_hotels_are_ranked_descending(tmp_path):
    """Em caso de empate no valor, ordena pelo id do hotel ascendente."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H03", "hotel_name": "Hotel A", "amount": "1000.00"},
            {"reservation_id": "R-2", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "1000.00"},
            {"reservation_id": "R-3", "hotel_id": "H04", "hotel_name": "Hotel C", "amount": "1000.00"},
            {"reservation_id": "R-4", "hotel_id": "H01", "hotel_name": "Hotel D", "amount": "1000.00"},
        ],
        top=3,
    )
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02", "H03"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["1000.00", "1000.00", "1000.00"]
