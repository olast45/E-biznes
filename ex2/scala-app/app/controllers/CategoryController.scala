package controllers

import javax.inject._
import play.api._
import play.api.libs.json._
import play.api.mvc._

import models.Category

@Singleton
class CategoryController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {

    var categories = scala.collection.mutable.ListBuffer.empty[Category]
    var currentId = 0 // Autoincrementing id

    def showAll() = Action { implicit request: Request[AnyContent] => 

        if (categories.isEmpty) {
            NotFound("There are no categories to be displayed!")

        } else {

            val categoriesJS: JsArray = JsArray(
                categories.map(category => Json.obj(
                    "id" -> category.id,
                    "name" -> category.name,
                ))
            )
            
            Ok(categoriesJS)

        }
    }

    def showById(requestedId: Long) = Action { implicit request: Request[AnyContent] =>

        val foundCategory = categories.find(_.id == requestedId)

        foundCategory match {
            case Some(category) => Ok(Json.obj(
                "id" -> category.id,
                "name" -> category.name,
            ))
            case None => NotFound(s"Category with id=$requestedId not found!")
        }
    }


    def deleteCategory(requestedId: Long) = Action { implicit request: Request[AnyContent] =>

        val foundCategory = categories.find(_.id == requestedId)

        foundCategory match {
            case Some(category) => 
                categories -= category
                Ok(s"Category with id=$requestedId removed")

            case None => NotFound(s"Category with id=$requestedId not found!")
        }
    }

    def deleteAllCategories() = Action { implicit request: Request[AnyContent] =>

        if (categories.isEmpty) {
            NotFound("There are no categories to be deleted!")

        } else {

            categories.clear()

            Ok("All categories were deleted!")
        }
  
    }

    def updateCategory(requestedId: Long) = Action { implicit request: Request[AnyContent] =>

        request.body.asJson match {
            case Some(body) =>
                val nameOpt = (body \ "name").asOpt[String]

                val foundCategory = categories.indexWhere(_.id == requestedId)
                foundCategory match {
                    case index if index >= 0 =>
                        val category = categories(index)
                        val updatedCategory = category.copy(
                            name = nameOpt.getOrElse(category.name), 
                        )
                        categories.update(index, updatedCategory)

                        Ok(s"Category with id=$requestedId updated!")

                    case _ => NotFound(s"Category with id=$requestedId not found!")
                }

            case None => BadRequest("Request doesn't have a body!")
        }

    }

    def addCategory() = Action { implicit request: Request[AnyContent] =>
        request.body.asJson match {
            case Some(body) =>
                val nameOpt = (body \ "name").asOpt[String]

                nameOpt match {
                    case Some(name) =>
                        currentId += 1
                        val newCategory = Category(currentId, name)
                        categories += newCategory
                        Ok("Category added!")

                    case None =>
                        BadRequest("Required fields are missing!")
                }

            case None =>
                BadRequest("Request doesn't have a body!")
        }
    }


}
