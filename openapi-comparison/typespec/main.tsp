import "@typespec/http";
import "@typespec/openapi3";

using TypeSpec.Http;

@service(#{
  title: "Library Management API (TypeSpec)",
  version: "1.0.0"
})
@server("http://localhost:5007", "Local server")
namespace Library;

model ErrorResponse {
  error: string;
}

model Book {
  id: int32;
  title: string;
  author: string;
  available: boolean;
}

model NewBook {
  title: string;
  author: string;
}

model NewLoan {
  bookId: int32;
  memberName: string;
}

model Loan {
  id: int32;
  bookId: int32;
  memberName: string;
  borrowedAt: utcDateTime;
}

@route("/books")
interface BooksApi {
  @get
  listBooks(): Book[];

  @post
  createBook(@body body: NewBook): Book | ErrorResponse;

  @get
  @route("/{bookId}")
  getBook(@path bookId: int32): Book | ErrorResponse;
}

@route("/loans")
interface LoansApi {
  @post
  createLoan(@body body: NewLoan): Loan | ErrorResponse;

  @delete
  @route("/{loanId}")
  deleteLoan(@path loanId: int32): void | ErrorResponse;
}
