import BaseModel from "./base_model.ts";

export type ArticlesFavoritesEntity = {
  article_id: number;
  user_id: number;
  id?: number;
  value: boolean;
};

/**
 * @description
 * Returns an instance of the ArticlesFavoritesModel
 *
 * @param ArticlesFavoritesEntity inputObj
 *
 * @return ArticlesFavoritesModel An instance of the model with all properties set
 */
export function createArticlesFavoritesModelObject(
  inputObj: ArticlesFavoritesEntity,
): ArticlesFavoritesModel {
  return new ArticlesFavoritesModel(
    inputObj.article_id,
    inputObj.user_id,
    inputObj.value,
    inputObj.id,
  );
}

export class ArticlesFavoritesModel extends BaseModel {
  //////////////////////////////////////////////////////////////////////////////
  // FILE MARKER - PROPERTIES //////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////

  /**
   * @var number
   *
   * id of the associated article in the database
   */
  public article_id: number;

  /**
   * @var number
   *
   * Id of the associated user in the database
   */
  public user_id: number;

  /**
   * @var number
   *
   * Id of the database row
   */
  public id: number;

  /**
   * @var boolean
   *
   * TODO(ebebbington) What is this property used for?
   */
  public value: boolean;

  /**
   * TODO(ebebbington) What is this property used for?
   */
  public query: string = "";

  //////////////////////////////////////////////////////////////////////////////
  // FILE MARKER - CONSTRCUTOR /////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////

  /**
   * @param number articleId
   * @param number authorId
   * @param boolean value
   * @param number id=-1
   */
  constructor(
    articleId: number,
    authorId: number,
    value: boolean,
    id: number = -1,
  ) {
    super();
    this.article_id = articleId;
    this.user_id = authorId;
    this.value = value;
    this.id = id;
  }

  //////////////////////////////////////////////////////////////////////////////
  // FILE MARKER - METHODS - CRUD //////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////

  /**
   * Delete this model.
   *
   * @return Promise<boolean>
   */
  public async delete(): Promise<boolean> {
    let query = `DELETE FROM articles WHERE id = ?`;
    query = this.prepareQuery(
      query,
      [
        String(this.id),
      ],
    );

    try {
      const client = await BaseModel.connect();
      await client.query(query);
      client.release();
    } catch (error) {
      console.log(error);
      return false;
    }
    return true;
  }

  /**
   * Save this model.
   *
   * @return Promise<ArticlesFavoritesModel>
   */
  public async save(): Promise<ArticlesFavoritesModel> {
    // If this model already has an ID, then that means we're updating the model
    if (this.id != -1) {
      return this.update();
    }

    let query = "INSERT INTO articles_favorites " +
      " (article_id, user_id, value)" +
      " VALUES (?, ?, ?);";
    query = this.prepareQuery(
      query,
      [
        String(this.article_id),
        String(this.user_id),
        String(this.value),
      ],
    );

    const client = await BaseModel.connect();
    await client.query(query);
    client.release();

    // @ts-ignore
    // (crookse) We ignore this because this will never return null.
    return ArticlesFavoritesModel.where({ article_id: this.article_id });
  }

  /**
   * Update this model.
   *
   * @return Promise<ArticlesFavoritesModel>
   */
  public async update(): Promise<ArticlesFavoritesModel> {
    let query = "UPDATE articles_favorites SET " +
      "value = ? " +
      `WHERE id = '${this.id}';`;
    query = this.prepareQuery(
      query,
      [
        String(this.value),
      ],
    );
    const client = await BaseModel.connect();
    await client.query(query);
    client.release();

    // @ts-ignore
    // (crookse) We ignore this because this will never return null.
    return ArticlesFavoritesModel.where({ article_id: this.article_id });
  }

  //////////////////////////////////////////////////////////////////////////////
  // FILE MARKER - METHODS - STATIC ////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////

  /**
   * @description
   *     See BaseModel.where()
   *
   * @param any fields
   *
   * @return Promise<ArticlesFavoritesModel[]|[]>
   */
  static async where(
    fields: any,
  ): Promise<ArticlesFavoritesModel[] | []> {
    let results = await BaseModel.where("articles_favorites", fields);

    if (results.length <= 0) {
      return [];
    }

    return results.map((result: any) => {
      return createArticlesFavoritesModelObject(result);
    });
  }

  /**
   * @description
   *     See BaseModel.whereIn()
   *
   * @param string column
   * @param any values
   *
   * @return Promise<ArticlesFavoritesModel[]|[]>
   */
  static async whereIn(
    column: string,
    values: any,
  ): Promise<ArticlesFavoritesModel[] | []> {
    let results = await BaseModel.whereIn("articles_favorites", {
      column,
      values,
    });

    if (results.length <= 0) {
      return [];
    }

    return results.map((result: any) => {
      return createArticlesFavoritesModelObject(result);
    });
  }

  //////////////////////////////////////////////////////////////////////////////
  // FILE MARKER - METHODS - PUBLIC ////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////

  /**
   * @description
   * Constructs an object of this models properties
   *
   * @return ArticlesFavoritesEntity
   */
  public toEntity(): ArticlesFavoritesEntity {
    return {
      id: this.id,
      article_id: this.article_id,
      user_id: this.user_id,
      value: this.value,
    };
  }
}
