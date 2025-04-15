package controllers

import (
	"myapp/models"
	"net/http"
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/labstack/echo/v4"
	"github.com/go-playground/validator/v10"
	"gorm.io/gorm"
)

type CartController struct{}

func (cc *CartController) GetCartById(c echo.Context) error {
	id := c.Param("id")
	db := c.Get("db").(*gorm.DB)

	var cart models.Cart

	if _, err := strconv.Atoi(id); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Id should be an integer!",
		})
	}

	if err := db.First(&cart, id).Error; err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": fmt.Sprintf("Cart with id=%s not found", id),
		})
	}

	return c.JSON(http.StatusOK, cart)
}

func (cc *CartController) GetAllCarts(c echo.Context) error {
	db := c.Get("db").(*gorm.DB)

	var carts []models.Cart

	if len := db.Find(&carts).RowsAffected ; len == 0 {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": "There are no carts to be displayed",
		})
	}

	return c.JSON(http.StatusOK, carts)
}

func (cc *CartController) CreateCart(c echo.Context) error {
	db := c.Get("db").(*gorm.DB)

	var cart models.Cart

	decoder := json.NewDecoder(c.Request().Body)
	decoder.DisallowUnknownFields()

	if err := decoder.Decode(&cart); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Invalid JSON payload",
		})
	}

	if err := validator.New().Struct(&cart); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": err.Error(),
		})
	}

	if err := db.Create(&cart).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Could not create cart",
		})
	}

	return c.JSON(http.StatusCreated, cart)
}

func (cc *CartController) UpdateCart(c echo.Context) error {
	id := c.Param("id")
	db := c.Get("db").(*gorm.DB)

	var cart models.Cart

	if _, err := strconv.Atoi(id); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Id should be an integer!",
		})
	}

	if err := db.First(&cart, id).Error; err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": fmt.Sprintf("Cart with id=%s not found", id),
		})
	}

	var updates map[string]interface{}
	decoder := json.NewDecoder(c.Request().Body)
	decoder.DisallowUnknownFields()

	if err := decoder.Decode(&updates); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Invalid JSON payload",
		})
	}

	if err := db.Model(&cart).Updates(updates).Error; err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to update cart",
		})
	}

	return c.JSON(http.StatusOK, cart)
}

func (cc *CartController) DeleteCart(c echo.Context) error {
	id := c.Param("id")
	db := c.Get("db").(*gorm.DB)

	var cart models.Cart

	if _, err := strconv.Atoi(id); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Id should be an integer!",
		})
	}

	if err := db.First(&cart, id).Error; err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": fmt.Sprintf("Cart with id=%s not found", id),
		})
	}

	db.Delete(&cart)


	return c.JSON(http.StatusOK, fmt.Sprintf("Cart with id=%s deleted", id))
}

func (cc *CartController) DeleteAllCarts(c echo.Context) error {
	db := c.Get("db").(*gorm.DB)

	db.Exec("DELETE FROM carts")

	return c.JSON(http.StatusOK, "All carts deleted!")
}
