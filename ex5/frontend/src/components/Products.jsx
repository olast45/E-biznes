import React, { useEffect, useState } from "react";

function Products() {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8080/products")
      .then((response) => {
        if (!response.ok) throw new Error("Błąd podczas pobierania produktów");
        return response.json();
      })
      .then((data) => setProducts(data))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div className="form-wrapper">
      <h2>Produkty</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {products.length === 0 ? (
        <p>Ładowanie produktów...</p>
      ) : (
        <ul>
          {products.map((product, index) => (
            <li key={index}>
              <strong>{product.name}</strong> – {product.price} zł
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Products;
