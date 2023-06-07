    # connection.execute("""
    #                    create table Customer(
    #                        Id integer primary key autoincrement,
    #                        Name text,
    #                        PathFile text
    #                        )""")
    # connection.execute("""
    #                    create table Signature(
    #                        Id integer primary key autoincrement,
    #                        IdCustomer integer not null,
    #                        PathSignature text,
    #                        Embedding text,
    #                        SignatureImage text
    #                    )
    #                    """)

class Signature:
    def __init__(self,Id,IdCustomer,PathSignature,Embedding,SignatureImage):
        self.Id = Id
        self.IdCustomer = IdCustomer
        self.PathSignature= PathSignature
        self.Embedding = Embedding
        self.SignatureImage = SignatureImage