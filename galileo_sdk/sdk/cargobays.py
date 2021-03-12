class CargoBaysSdk:
    def __init__(self, cargo_bays_service):
        self._cargo_bays_service = cargo_bays_service

    def list_cargobays(self):
        """
        Get list of CargoBays associated with your account

        :return: List[CargoBay]
        
        Example:
            >>> cargobays = galileo.cargobays.list_cargobays()
            >>> for cargobay in cargobays:
            >>>    print(cargobay.name)
        """
        return self._cargo_bays_service.list_cargobays()