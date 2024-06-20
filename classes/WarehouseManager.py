from multiprocessing import Process, Manager


class WarehouseManager:
    def __init__(self):
        self.__data = Manager().dict()

    def process_request(self, request):
        product, action, quantity = request
        if action == "receipt":
            self.__data[product] = self.__data.get(product, 0) + quantity
        elif action == "shipment":
            if product in self.__data and self.__data[product] >= quantity:
                self.__data[product] -= quantity

    def run(self, requests):
        processes = []
        for request in requests:
            p = Process(target=self.process_request, args=(request,))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

    @property
    def data(self):
        return dict(self.__data)



